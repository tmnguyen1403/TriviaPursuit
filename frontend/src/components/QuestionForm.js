import React, { useState } from 'react';
import './QuestionForm.css';

const QuestionForm = ({ question, onSave }) => {
  const [category, setCategory] = useState(question.category);
  const [type, setType] = useState(question.type);
  const [content, setContent] = useState(question.content);
  const [answer, setAnswer] = useState(question.answer);
  const [link, setLink] = useState(question.link);

  const handleCategoryChange = (e) => {
    setCategory(e.target.value);
  };

  const handleTypeChange = (e) => {
    setType(e.target.value);
  };

  const handleContentChange = (e) => {
    setContent(e.target.value);
  };

  const handleAnswerChange = (e) => {
    setAnswer(e.target.value);
  };

  const handleLinkChange = (e) => {
    setLink(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate and save the edited question
    if (content.trim() === '' || answer.trim() === '') {
      alert('Please enter both question and answer');
    } else {
      onSave({ ...question, content, answer, category, type, link });
    }
  };

  const handleInputClick = (e) => {
    e.target.value = ''; // Clear the input value
  };

  return (
    <form onSubmit={handleSubmit} className="question-form">
      <label>
        Category:
        <input type="text" value={category} onChange={handleCategoryChange} onClick={handleInputClick} />
      </label>
      <label>
        Type:
        <input type="text" value={type} onChange={handleTypeChange} onClick={handleInputClick} />
      </label>
      <label>
        Question:
        <input type="text" value={content} onChange={handleContentChange} onClick={handleInputClick} />
      </label>
      <label>
        Answer:
        <input type="text" value={answer} onChange={handleAnswerChange} onClick={handleInputClick} />
      </label>
      <label>
        Link:
        <input type="text" value={link} onChange={handleLinkChange} onClick={handleInputClick} />
      </label>
      <button type="submit">Save</button>
    </form>
  );
};

export default QuestionForm;
