import { Link } from 'react-router-dom'

const Signup = () => {

    return (
        <div className="container">
            <h2 className="text-center">Trivial Compute</h2>
            <h3 className="text-center">Create Account</h3>
            <form>
            <div className="form-group">
                <label className="form-label" for="username">Full Name:</label>
                <input type="text" className="form-control" id="name" name="name" required />
            </div>
            <div className="form-group">
                <label className="form-label" for="username">Username:</label>
                <input type="text" className="form-control" id="username" name="username" required />
            </div>
            <div className="form-group">
                <label className="form-label" for="username">Email:</label>
                <input type="email" className="form-control" id="email" name="email" required />
            </div>
            <div className="form-group">
                <label className="form-label" for="password">Password:</label>
                <input type="password" className="form-control" id="password" name="password" required />
            </div>
            <div class="col-12">
                <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
            </div>
            
            </form>
            
            <h4 className="text-center">Already have an account? <Link to="/login">Log in</Link></h4>
        </div>
    )
}

export default Signup;
