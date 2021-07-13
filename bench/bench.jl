using Statistics

function board(X_0::Array, b::Float64)

    x0 = copy(X_0[1])
    y0 = copy(X_0[2])
    u0 = copy(X_0[3])
    v0 = copy(X_0[4])

    g = 9.81
    c = 0.5
    a = 0.25
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


function runge_kutta_step(f::Function, x0, dt::Float64, t=nothing)

    k1 = f(x0, t) * dt
    k2 = f(x0 + k1/2, t) * dt
    k3 = f(x0 + k2/2, t) * dt
    k4 = f(x0 + k3, t) * dt
    x_new = x0 + (k1 + 2*k2 + 2*k3 + k4)/6

    return x_new
end


function solver(f::Function, x0::Array, y0::Array, u0::Array, v0::Array, dt::Float64, N_t::Int, b = 0.5)
    solutions = []
    for k in 1:length(x0)
        values_one_step = [x0[k], y0[k], u0[k], v0[k]]
        for i in 2:N_t + 1
            values_one_step = runge_kutta_step(f, values_one_step, dt, b)
        end
        solutions = vcat(solutions, values_one_step)
    end

    return solutions
end


function bench(n_sleds, n_time)
    x_init = zeros(n_sleds)
    y_init = rand(n_sleds)
    u_init = zeros(n_sleds)
    v_init = zeros(n_sleds) .+ 3.5

    return solver(board, x_init, y_init, u_init, v_init, 0.01, n_time)
end


n_sleds = 10
n_time = 200

nb_runs = 200

times = zeros(nb_runs)

for irun in 1:nb_runs
    times[irun] = @elapsed bench(n_sleds, n_time)
end

println(median(times))
