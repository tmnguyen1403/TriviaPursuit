import React, { useState, useEffect } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import axios from "axios";

import Loading from "../components/Loading";

const QuestionEdit = () => {
  const navigate = useNavigate();
  let { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [content, setContent] = useState({});

  useEffect(() => {
    const editData = async () => {
      try {
        const res = await axios.get(
          `http://localhost:9000/api/questions/${id}`
        );
        console.log(res);
        setContent(res.data.obtainedQuestion);
        setLoading(false);
      } catch (err) {
        console.error(err);
      }
    };
    editData();
  }, [id]);

  const handleInput = (event) => {
    event.persist();
    setContent({ ...content, [event.target.name]: event.target.value });
  };

  const updateQuestion = async (event) => {
    event.preventDefault();
    setLoading(true);
    const data = {
      category: content.category,
      type: content.type,
      link: content.link,
      question: content.question,
      answer: content.answer,
      user_id: content.user_id,
    };

    await axios
      .patch(`http://localhost:9000/api/questions/${id}`, data)
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
                  Edit Question
                  <Link to="/" className="btn btn-danger float-end">
                    Back
                  </Link>
                </h4>
              </div>
              <div className="card-body">
                <form onSubmit={updateQuestion}>
                  <div className="mb-3">
                    <label>
                      Category <span style={{ color: "red" }}>*</span>
                    </label>
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
                    <label>
                      Type <span style={{ color: "red" }}>*</span>
                    </label>
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
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  {content.type === "Video" && (
                    <div className="mb-3">
                      <label>Link</label>
                      <input
                        type="text"
                        name="link"
                        value={content.link}
                        onChange={handleInput}
                        className="form-control"
                      />
                    </div>
                  )}
                  {content.type === "Audio" && (
                    <div className="mb-3">
                      <label>Link</label>
                      <input
                        type="text"
                        name="link"
                        value={content.link}
                        onChange={handleInput}
                        className="form-control"
                      />
                    </div>
                  )}
                  {content.type === "Other" && (
                    <div className="mb-3">
                      <label>Link</label>
                      <input
                        type="text"
                        name="link"
                        value={content.link}
                        onChange={handleInput}
                        className="form-control"
                      />
                    </div>
                  )}
                  <div className="mb-3">
                    <label>
                      Question <span style={{ color: "red" }}>*</span>
                    </label>
                    <input
                      type="text"
                      name="question"
                      value={content.question}
                      onChange={handleInput}
                      className="form-control"
                    />
                  </div>
                  <div className="mb-3">
                    <label>
                      Answer <span style={{ color: "red" }}>*</span>
                    </label>
                    <input
                      type="text"
                      name="answer"
                      value={content.answer}
                      onChange={handleInput}
                      className="form-control"
                    />
                  </div>
                  <div>
                    <p style={{ color: "red", textAlign: "right" }}>
                      * Required
                    </p>
                  </div>
                  <div class="mb-3">
                    <button type="submit" className="btn btn-primary">
                      Update
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

export default QuestionEdit;
