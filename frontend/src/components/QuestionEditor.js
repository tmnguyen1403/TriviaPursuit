import React, { useState } from 'react';
import QuestionForm from './QuestionForm.js';
import './QuestionEditor.css';

const QuestionEditor = () => {
  const [questions, setQuestions] = useState([
    { id: 1, 
        category: 'Math', 
        type: 'Text', 
        content: '1+1', 
        answer: '2', 
        link: 'if any'}
  ]);

  const handleQuestionSave = (editedQuestion) => {
    const updatedQuestions = questions.map((question) =>
      question.id === editedQuestion.id ? editedQuestion : question
    );
    setQuestions(updatedQuestions);
  };

  return (
    <div>
      <header className="header">
        <h1>Trivial Compute</h1>
        <p>A web application for learning and teaching</p>
      </header>
      {questions.map((question) => (
        <QuestionForm key={question.id} question={question} onSave={handleQuestionSave} />
      ))}
    </div>
  );
};

export default QuestionEditor;
