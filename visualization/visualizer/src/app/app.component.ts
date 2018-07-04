import { Component } from '@angular/core';
declare var d3;
declare var PIXI;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.styl']
})
export class AppComponent {
    data:any;

    /*
     * Opens the file selected by the user, parses the JSON and saves contents
     * in memory.
     */
    open(input) {
        let file = input.files[0];
        let reader = new FileReader();
        reader.onload = this.display;
        reader.readAsText(file);
    }

    display(e) {
        var contents = e.target.result;
        this.data = JSON.parse(contents);
        let graph = this.data;

        // Setting up the PIXI canvas
        let canvas = document.getElementById("canvas");
        var positionInfo = canvas.getBoundingClientRect();
        var height = positionInfo.height-3;
        var width = positionInfo.width-3;
        let stage = new PIXI.Container();
        let renderer = PIXI.autoDetectRenderer(
            width,
            height,
            {
                antialias: true,
                transparent: true,
                resolution: 1
            }
        );
        canvas.appendChild(renderer.view);

        // Defines the color of the nodes
        let colour = (function() {
            let scale = d3.scaleOrdinal(d3.schemeCategory20);
            return (num) => parseInt(scale(num).slice(1), 16);
        })();

        // Defines the simulation forces
        let simulation = d3.forceSimulation()
            .force('link', d3.forceLink().id((d) => d.id))              // Harmonic spring
            .force('charge', d3.forceManyBody().strength(-30))          // Long-range charge
            .force('center', d3.forceCenter(width / 2, height / 2));    // Centering force

        // A layer for drawing links
        let links = new PIXI.Graphics();
        stage.addChild(links);

        // Defines the node style
        graph.nodes.forEach((node) => {
            node.gfx = new PIXI.Graphics();
            node.gfx.lineStyle(1.5, 0xFFFFFF);
            node.gfx.beginFill(colour(node.group));
            node.gfx.drawCircle(0, 0, 5);
            stage.addChild(node.gfx);
        });

        d3.select(renderer.view)
            .call(d3.drag()
                .container(renderer.view)
                .subject(() => simulation.find(d3.event.x, d3.event.y))
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));

        // Define that on each simulations step the rendering is called
        simulation
            .nodes(graph.nodes)
            .on('tick', render);

        simulation.force('link')
            .links(graph.links);

        // Rendering loop
        function render() {

            // Moves nodes
            graph.nodes.forEach((node) => {
                let { x, y, gfx } = node;
                gfx.position = new PIXI.Point(x, y);
            });

            // Draws lines
            links.clear();
            links.alpha = 0.6;
            graph.links.forEach((link) => {
                let { source, target } = link;
                links.lineStyle(Math.sqrt(link.value), 0x999999);
                links.moveTo(source.x, source.y);
                links.lineTo(target.x, target.y);
            });
            links.endFill();

            renderer.render(stage);
        }

        // Handles start of drag
        function dragstarted() {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d3.event.subject.fx = d3.event.subject.x;
            d3.event.subject.fy = d3.event.subject.y;
        }

        // Handles drag
        function dragged() {
            d3.event.subject.fx = d3.event.x;
            d3.event.subject.fy = d3.event.y;
        }

        // Handles end of drag
        function dragended() {
            if (!d3.event.active) simulation.alphaTarget(0);
            d3.event.subject.fx = null;
            d3.event.subject.fy = null;
        }
    }
}
