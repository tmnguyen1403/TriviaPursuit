import { Link } from "react-router-dom";

const Login = () => {
  return (
    <div class="container mt-5">
      <div className="row justify-content-center">
        <div className="col-sm-4">
          <div className="card">
            <div className="card-body">
              <h3 className="card-title text-center">Login</h3>
              <form>
                <div className="mb-3">
                  <label for="email">Email</label>
                  <input
                    type="text"
                    className="form-control"
                    id="email"
                    placeholder="Enter your email"
                  />
                </div>
                <div className="mb-4">
                  <label for="password">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    placeholder="Enter your password"
                  />
                </div>
                <div className="mb-3 d-grid gap-2 col-4 mx-auto">
                  <button type="submit" className="btn btn-primary btn-block rounded-pill">
                    Login
                  </button>
                </div>
              </form>
            </div>
            <div class="card-footer text-center">
              <p>
                Need an account? <Link to="/sign-up">Sign up here</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
