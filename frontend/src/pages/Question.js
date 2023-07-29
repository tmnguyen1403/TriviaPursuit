import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Loading from '../components/Loading';

const Question = () => {

    const [loading, setLoading] = useState([]);
    const [questions, setQuestions] = useState([]);

    useEffect(() => {
      const fetchData = async () => {
        try {
          const res = await axios.get(
            `http://localhost:9000/api/questions/user/64b38cd889ebea252ec03ab2`
          );
          console.log(res);
          setQuestions(res.data.questionsByUserId);
          setLoading(false);
        } catch (err) {
          console.error(err);
        }
      };
      fetchData();
    }, []);

    const deleteQuestion = (e, id) => {
      e.preventDefault();

      const thisClicked = e.currentTarget;
      thisClicked.innerText = "Deleting...";

      axios.delete(`http://localhost:9000/api/questions/${id}`)
            .then(res => {
                thisClicked.closest('tr').remove();
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }


    if (loading) {
      return (
        <div>
          <Loading />
        </div>
      )
    }

    var questionDetails = "";
    questionDetails = questions.map((item, index) => {
        return (
            <tr key={index}>
                <td>{item.category}</td>
                <td>{item.type}</td>
                <td>{item.question}</td>
                <td>{item.answer}</td>
                <td>{item.createdAt}</td>
                <td>
                    <Link to={`/questions/${item._id}/edit`} className="btn btn-success">Edit</Link>
                </td>
                <td>
                    <button type="button" onClick={(e) => deleteQuestion(e, item._id)} className="btn btn-danger">Delete</button>
                </td>
            </tr>
        )
    });


    return (
      <div className="container mt-5">
        <div className="row">
          <div className="col-md-12">
            <div className="card">
              <div className="card-header">
                <h4>
                  Questions List
                  <Link to="/questions/create" className="btn btn-primary float-end">
                    Add Question
                  </Link>
                </h4>
              </div>
              <div className="card-body">
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th>Category</th>
                      <th>Type</th>
                      <th>Question</th>
                      <th>Answer</th>
                      <th>Created At</th>
                      <th>Edit</th>
                      <th>Delete</th>
                    </tr>
                  </thead>
                  <tbody>
                    {questionDetails}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
}

export default Question;