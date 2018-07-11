import { Component } from '@angular/core';
declare var d3;
declare var PIXI;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.styl']
})
export class AppComponent {

    initialGraph:any;
    graph:any;
    charge:number = -4;
    distance:number = 20;
    threshold:number = 5;
    simulation:any;
    renderer:any;
    stage:any;
    links:any;
    width:number;
    height:number;
    colour:any;
    lastPos:any = null;
    offset:any;
    info:any;
    root:any;

    /*
     * Opens the file selected by the user, parses the JSON and saves contents
     * in memory.
     */
    open(input) {
        let file = input.files[0];
        let reader = new FileReader();
        reader.onload = this.display.bind(this);
        reader.readAsText(file);
    }

    /*
     * Used to change the charge that controls the amount of long range
     * interaction between nodes.
     */
    changeCharge(value:number) {
        this.simulation.force("charge").strength(value)
        this.charge = value;

        // Restarts the simulation (important if simulation has already slowed down)
        this.simulation.alpha(1).restart();
    }

    /*
     * Used to change the charge that controls the amount of long range
     * interaction between nodes.
     */
    changeDistance(value:number) {
        this.simulation.force("link")
            .id(function(d) {
                return d.id;
            })
            .distance(value)
        this.distance = value;

        // Restarts the simulation (important if simulation has already slowed down)
        this.simulation.alpha(1).restart();
    }

    /*
     * Used to change the charge that controls the amount of long range
     * interaction between nodes.
     */
    changeThreshold(value:number) {

        // Disable the links according to the threshold that was set.
        this.threshold = value;
        let validLinks = this.getValidLinks(this.initialGraph.links, value);
        this.graph.links = validLinks;
        this.simulation.force('link')
            .links(validLinks);

        // Restarts the simulation (important if simulation has already slowed down)
        this.simulation.alpha(1).restart();
    }

    getValidLinks(links, threshold) {
        // Disable the links according to the threshold that was set.
        let newLinks = [];
        for (let link of links) {
            if (link.value <= threshold) {
                newLinks.push(link);
            }
        }
        return newLinks;
    }

    display(e) {
        var contents = e.target.result;
        this.initialGraph = JSON.parse(contents);
        this.graph = Object.assign({}, this.initialGraph);

        // Setting up the PIXI canvas
        let canvas = document.getElementById("canvas");
        var positionInfo = canvas.getBoundingClientRect();
        this.height = positionInfo.height-3;
        this.width = positionInfo.width-3;
        this.stage = new PIXI.Container();
        this.root = new PIXI.Container();
        this.stage.addChild(this.root);
        this.renderer = PIXI.autoDetectRenderer(
            this.width,
            this.height,
            {
                antialias: true,
                transparent: true,
                resolution: 1
            }
        );
        canvas.appendChild(this.renderer.view);

        // Defines the color of the nodes
        this.colour = (function() {
            let scale = d3.scaleOrdinal(d3.schemeCategory20);
            return (num) => parseInt(scale(num).slice(1), 16);
        })();

        // A layer for drawing links
        this.links = new PIXI.Graphics();
        this.root.addChild(this.links);

        // Show information when mouse is over it
        // Designate circle as being interactive so it handles events
        this.stage.interactive = true;

        // Create hit area, needed for interactivity
        this.stage.hitArea = new PIXI.Rectangle(0, 0, this.width, this.height);
        this.stage.component = this;
        this.stage.mousedown = function(mouseData) {
            this.component.hideInfo();
        }

        this.update();
        this.changeThreshold(this.threshold);
        this.animate();
    }

    showInfo(info) {
        this.info = info;
    }

    hideInfo() {
        this.info = null;
    }

    update() {
        // Defines the simulation forces
        let simulation = d3.forceSimulation()
            .force('link', d3.forceLink().id((d) => d.id).distance(this.distance))               // Link distance
            .force('charge', d3.forceManyBody().strength(this.charge))                           // Long-range charge
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))                    // Centering force
            .force('radial', d3.forceRadial(0, this.width / 2, this.height / 2).strength(0.01)); // Radial force towards origin
        this.simulation = simulation;

        // Defines the node style
        this.graph.nodes.forEach((node) => {
            node.gfx = new PIXI.Graphics();
            node.gfx.lineStyle(1.5, 0xFFFFFF);
            node.gfx.beginFill(this.colour(node.lattice_system));
            node.gfx.drawCircle(0, 0, 5);

            // Designate circle as being interactive so it handles events
            node.gfx.interactive = true;

            // Create hit area, needed for interactivity
            node.gfx.hitArea = new PIXI.Circle(0, 0, 5);

            node.gfx.component = this;
            node.gfx.node = node;

            // Show information when mouse is over it
            node.gfx.mousedown = function(mouseData) {
                console.log("Pixi");
                this.component.showInfo(this.node);
                mouseData.stopPropagation();
            }

            this.root.addChild(node.gfx);
        });

        d3.select(this.renderer.view)
            .call(d3.drag()
                .container(this.renderer.view)
                .subject(() => simulation.find(d3.event.x- this.root.x, d3.event.y-this.root.y))
                .on('start', this.dragstarted.bind(this))
                .on('drag', this.dragged.bind(this))
                .on('end', dragended));

        // Define that on each simulations step the rendering is called
        simulation
            .nodes(this.graph.nodes)
            .on('tick', this.render.bind(this));

        // Defining the links here slows down the visualization for some
        // reason. Instead when the links aer defined after this function, the
        // visualization is smoother.
        //let validLinks = this.getValidLinks(this.graph.links, this.threshold);
        //simulation.force('link')
            //.links(validLinks);

        // Handles end of drag
        function dragended() {
            if (!d3.event.active) simulation.alphaTarget(0);
            d3.event.subject.fx = null;
            d3.event.subject.fy = null;
        }
    }

    // Handles start of drag
    dragstarted() {
        if (!d3.event.active) {
            this.simulation.alphaTarget(0.3).restart();
        }
        d3.event.subject.fx = d3.event.subject.x;
        d3.event.subject.fy = d3.event.subject.y;
    }

    // Handles node draggin
    dragged() {
        d3.event.subject.fx = d3.event.x;
        d3.event.subject.fy = d3.event.y;
    }

    mouseDown(e) {
        e.preventDefault();
        this.lastPos = {x:e.offsetX, y:e.offsetY};
    }

    mouseUp(e) {
        this.lastPos = null;
    }

    mouseMove(e) {
        if (this.lastPos) {
            this.root.x += (e.offsetX-this.lastPos.x);
            this.root.y += (e.offsetY-this.lastPos.y);
            this.lastPos = {x: e.offsetX, y: e.offsetY};
            this.render();  // We need to ask for manual render
        }
    }

    // Rendering loop
    render() {
        // Moves nodes
        this.graph.nodes.forEach((node) => {
            let { x, y, gfx } = node;
            gfx.position = new PIXI.Point(x, y);
        });

        // Draws lines
        this.links.clear();
        this.links.alpha = 0.6;
        this.graph.links.forEach((link) => {
            let { source, target } = link;
            this.links.lineStyle(Math.sqrt(link.value), 0x999999);
            this.links.moveTo(source.x, source.y);
            this.links.lineTo(target.x, target.y);
        });
        this.links.endFill();

        this.renderer.render(this.stage);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.renderer.render(this.stage);
    }
}
