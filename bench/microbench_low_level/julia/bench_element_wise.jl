using Statistics

function element_wise(arr::Array)

    dt = 0.1
    x0 = arr

    k1 = x0 * dt
    k2 = (x0 + k1 / 2) * dt
    k3 = (x0 + k2 / 2) * dt
    k4 = (x0 + k3) * dt
    x_new = x0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return x_new

end

compute_from_arr = element_wise

size = 4
nb_runs = 2000

times = zeros(nb_runs)

for irun in 1:nb_runs
    arr = rand(size)
    times[irun] = @elapsed compute_from_arr(arr)
end

println(median(times))
