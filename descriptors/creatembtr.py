"""
An example on how to efficiently create the MBTR descriptor by using multiple
processes.
"""
import multiprocessing

from scipy.sparse import lil_matrix


def create(data):
    """This is the function that is called by each process but with different
    parts of the data -> data parallellism
    """
    global dataset
    global mbtr
    i_part = data[0]
    samples = data[1]
    n_samples = len(samples)
    n_features = int(mbtr.get_number_of_features())
    mbtr_inputs = lil_matrix((n_samples, n_features))

    # Create descriptors for the dataset
    for i_sample, sample_id in enumerate(samples):

        print("{} %".format(i_sample/n_samples*100))
        # Set charges and create descriptors
        sample = dataset[sample_id]
        system = sample["atoms"]
        system.charges = system.numbers
        mbtr_mat = mbtr.create(system)
        mbtr_inputs[i_sample, :] = mbtr_mat

    # Return the list of features for each sample
    return {
        "part": i_part,
        "mbtr": mbtr_inputs,
    }


def split(items, n):
    """
    """
    k, m = divmod(len(items), n)
    splitted = (items[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
    return splitted


def create_parallel(param_dataset, ncores, nsamples, param_mbtr):

    # Split the data into roughly equivalent chunks for each process. The entries
    global dataset
    dataset = param_dataset
    global mbtr
    mbtr = param_mbtr
    keys = sorted(list(dataset.keys()))
    if nsamples is None:
        n_samples = len(keys)
    keys = keys[:n_samples]
    samples_split = split(keys, ncores)
    id_samples_tuple = [(x[0], x[1]) for x in enumerate(samples_split)]

    # Initialize a pool of processes, and tell each process in the pool to
    # handle a different part of the data
    pool = multiprocessing.Pool(processes=ncores)
    results = pool.map(create, id_samples_tuple)

    # Sort results to the original order
    results = sorted(results, key=lambda x: x["part"])
    n_features = int(results[0]["mbtr"].shape[1])

    # Combine the results at the end when all processes have finished
    mbtr_list = lil_matrix((n_samples, n_features))
    i_id = 0
    for result in results:
        i_n_samples = result["mbtr"].shape[0]
        mbtr_in = result["mbtr"]
        mbtr_list[i_id:i_id+i_n_samples, :] = mbtr_in
        i_id += i_n_samples

    # Convert lil_matrix to CSR format. The lil format is good for creating a
    # sparse matrix, CSR is good for efficient math.
    mbtr_list = mbtr_list.tocsr()

    # Save results as a sparse matrix.
    return mbtr_list
