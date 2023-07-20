import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios';

import Loading from '../components/Loading';

const QuestionCreate = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [content, setContent] = useState({
        category: '',
        type:'',
        question: '',
        answer: '',
        user_id: ''
    })

    const handleInput = event => {
        event.persist();
        setContent({...content, [event.target.name]: event.target.value});
    }

    const saveQuestion = event => {
        event.preventDefault();
        setLoading(true);
        const data = {
            category: content.category,
            type: content.type,
            question: content.question,
            answer: content.answer,
            user_id: content.user_id
        }

        axios.post(`http://localhost:9000/api/questions`, data)
            .then(res => {
                navigate('/questions');
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    };

    if (loading) {
        return (
          <div>
            <Loading />
          </div>
        )
    }

    return (
      <div>
        <div className="container mt-5">
          <div className="row">
            <div className="col-md-12">
              <div className="card">
                <div className="card-header">
                  <h4>
                    Add Question
                    <Link
                      to="/questions"
                      className="btn btn-danger float-end"
                    >
                      Back
                    </Link>
                  </h4>
                </div>
                <div className="card-body">
                    <form onSubmit={saveQuestion}>
                        <div className="mb-3">
                            <label>Category</label>
                            <input type="text" name="category" value={content.category} onChange={handleInput} className="form-control" />
                        </div>
                        <div className="mb-3">
                            <label>Type</label>
                            <input type="text" name="type" value={content.type} onChange={handleInput} className="form-control" />
                        </div>
                        <div className="mb-3">
                            <label>Question</label>
                            <input type="text" name="question" value={content.question} onChange={handleInput} className="form-control" />
                        </div>
                        <div className="mb-3">
                            <label>Answer</label>
                            <input type="text" name="answer" value={content.answer} onChange={handleInput} className="form-control" />
                        </div>
                        <div className="mb-3">
                            <label>User ID</label>
                            <input type="text" name="user_id" value={content.user_id} onChange={handleInput} className="form-control" />
                        </div>
                        <div class="mb-3">
                            <button type="submit" className="btn btn-primary">Save</button>
                        </div>
                    </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
}

export default QuestionCreate;