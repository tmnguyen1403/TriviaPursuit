import { Link } from 'react-router-dom'

const Login = () => {

    return (
        <div className="container">
            <h2 className="text-center">Trivial Compute Question Management Center</h2>
            <h3 className="text-center">Login</h3>
            <form>
            <div className="form-group">
                <label className="form-label" for="username">Username:</label>
                <input type="text" className="form-control" id="username" name="username" required />
            </div>
            <div className="form-group">
                <label className="form-label" for="password">Password:</label>
                <input type="password" className="form-control" id="password" name="password" required />
            </div>
            <button type="submit" className="btn btn-primary btn-block">Login</button>
            </form>
            
            <h4 className="text-center">Need an account? <Link href="/sign-up">Sign up</Link></h4>
        </div>
    )
}

export default Login;
