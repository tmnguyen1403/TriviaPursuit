import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

import Loading from "../components/Loading";

const QuestionCreate = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [content, setContent] = useState({
    category: "",
    type: "",
    question: "",
    answer: "",
    user_id: "64b38cd889ebea252ec03ab2"
  });

  const handleInput = (event) => {
    event.persist();
    setContent({ ...content, [event.target.name]: event.target.value });
  };

  const saveQuestion = async (event) => {
    event.preventDefault();
    setLoading(true);
    const data = {
      category: content.category,
      type: content.type,
      question: content.question,
      answer: content.answer,
      user_id: content.user_id,
    };

    await axios
      .post(`http://localhost:9000/api/questions`, data)
      .then((res) => {
        navigate("/");
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  if (loading) {
    return (
      <div>
        <Loading />
      </div>
    );
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
                  <Link to="/" className="btn btn-danger float-end">
                    Back
                  </Link>
                </h4>
              </div>
              <div className="card-body">
                <form onSubmit={saveQuestion}>
                  <div className="mb-3">
                    <label>Category</label>
                    <select
                      type="text"
                      name="category"
                      value={content.category}
                      onChange={handleInput}
                      className="form-control"
                    >
                      <option value="">Select an option</option>
                      <option value="Math">Math</option>
                      <option value="History">History</option>
                      <option value="Sport">Sport</option>
                      <option value="Movie">Movie</option>
                      <option value="Geography">Geography</option>
                      <option value="Biology">Biology</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label>Type</label>
                    <select
                      type="text"
                      name="type"
                      value={content.type}
                      onChange={handleInput}
                      className="form-control"
                    >
                      <option value="">Select an option</option>
                      <option value="Text">Text</option>
                      <option value="Video">Video</option>
                      <option value="Audio">Audio</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label>Question</label>
                    <input
                      type="text"
                      name="question"
                      value={content.question}
                      onChange={handleInput}
                      className="form-control"
                    />
                  </div>
                  <div className="mb-3">
                    <label>Answer</label>
                    <input
                      type="text"
                      name="answer"
                      value={content.answer}
                      onChange={handleInput}
                      className="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <button type="submit" className="btn btn-primary">
                      Save
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionCreate;
