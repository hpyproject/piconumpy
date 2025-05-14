using Statistics


function cort(s1, s2)
    num = 0.0
    sum_square_x = 0.0
    sum_square_y = 0.0
    for t in 1:length(s1)-1
        slope_1 = s1[t + 1] - s1[t]
        slope_2 = s2[t + 1] - s2[t]
        num += slope_1 * slope_2
        sum_square_x += slope_1 * slope_1
        sum_square_y += slope_2 * slope_2
    end
    return num / (sqrt(sum_square_x * sum_square_y))
end

function use_cort(arr)
    return cort(arr, arr)
end


compute_from_arr = use_cort

size = 10000
nb_runs = 200

times = zeros(nb_runs)

for irun in 1:nb_runs
    arr = rand(size)
    times[irun] = @elapsed compute_from_arr(arr)
end

println(median(times))
