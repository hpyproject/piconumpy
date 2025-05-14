using Statistics

function instantiate(arr::Array)
    x = arr[1]
    result = [x, 3*x, 6*x, 9*x]
    result[1] = 2 * result[2]
    return result
end

compute_from_arr = instantiate

size = 4
nb_runs = 200

times = zeros(nb_runs)

for irun in 1:nb_runs
    arr = rand(size)
    times[irun] = @elapsed compute_from_arr(arr)
end

println(median(times))
