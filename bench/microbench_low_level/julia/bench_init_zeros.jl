using Statistics

function init_zeros(arr)
    for i in eachindex(arr)
        arr[i] = 0.0
    end
end

compute_from_arr = init_zeros

size = 4
nb_runs = 200

times = zeros(nb_runs)

for irun in 1:nb_runs
    arr = rand(size)
    times[irun] = @elapsed compute_from_arr(arr)
end

println(median(times))
