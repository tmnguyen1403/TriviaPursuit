import React, { useState } from 'react';
import { Link } from "react-router-dom";
 
const Signup = () => {

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-sm-6">
          <div className="card">
            <div className="card-body">
              <h3 className="card-title text-center">Create your account</h3>
              <form className='signup'>
                <div className="mb-3">
                  <label>Username</label>
                  <input
                    type="username"
                    className="form-control"
                    placeholder="Enter your username"
                  />
                </div>
                <div className="mb-3">
                  <label>Email</label>
                  <input
                    type="email"
                    className="form-control"
                    placeholder="Enter your email"
                  />
                </div>
                <div className="mb-4">
                  <label>Password</label>
                  <input
                    type="password"
                    className="form-control"
                    placeholder="Enter your password"
                  />
                </div>
                <div className="mb-3 d-grid gap-2 col-4 mx-auto">
                  <button type="submit" className="btn btn-primary btn-block rounded-pill">
                    Sign Up
                  </button>
                </div>
              </form>
            </div>
            <div class="card-footer text-center">
              <p>
                Already have an account? <Link to="/login">Login here</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
