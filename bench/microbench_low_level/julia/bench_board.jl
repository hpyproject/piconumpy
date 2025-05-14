using Statistics

function board(X_0::Array)

    x0 = copy(X_0[1])
    y0 = copy(X_0[2])
    u0 = copy(X_0[3])
    v0 = copy(X_0[4])

    g = 9.81
    a = 0.25
    b = 0.5
    c = 0.5
    p = (2*π)/10.0
    q = (2*π)/4.0

    H_x = -a + b*p*sin(p*x0)*cos(q*y0)
    H_xx = b*p^2 * cos(p*x0)*cos(q*y0)
    H_y = b*q*cos(p*x0)*sin(q*y0)
    H_yy = b*q^2 * cos(p*x0)*cos(q*y0)
    H_xy = -b*q*p*sin(p*x0)*sin(q*y0)

    F = (g + H_xx*u0^2 + 2*H_xy*u0*v0 + H_yy*v0^2)/(1 + H_x^2 + H_y^2)

    dU = -F*H_x - c*u0
    dV = -F*H_y - c*v0

    return [u0, v0, dU, dV]

end

compute_from_arr = board

size = 4
nb_runs = 200

times = zeros(nb_runs)

for irun in 1:nb_runs
    arr = rand(size)
    times[irun] = @elapsed compute_from_arr(arr)
end

println(median(times))
