const mongoose = require('mongoose');

const Question = require('../models/question');
const HttpError = require('../models/http-error');

const createQuestion = async(req, res, next) => {
    try {
        const {category, type, question, answer, link, user_id} = req.body;
        const createdQuestion = new Question({
            category,
            type,
            question,
            answer,
            link,
            user_id,
            createdAt: new Date()
        })
        await createdQuestion.save();
        res.status(201).json(createdQuestion);
    } catch (error) {
        res.status(500).json({message: error.message});
    }
}

const getQuestionById = async(req, res, next) => {
    const questionId = req.params.qid;
    let obtainedQuestion;
    try {
        obtainedQuestion = await Question.findById(questionId);
    }catch (err) {
        const error = new HttpError('Something went wrong, could not find the question Id.', 404);
        return next(error);
    } 

    if (!obtainedQuestion) {
        const error = new HttpError('Could not find a question for the provided Id', 404);
        return next(error);
    }

    res.status(201).json(obtainedQuestion);
}

const deleteQuestion = async(req, res, next) => {

    const questionId = req.params.qid;
    let obtainedQuestion;

    try {
        obtainedQuestion = await Question.findById(questionId);
    }catch (err) {
        const error = new HttpError('Something went wrong, could not delete the question.', 500);
        return next(error);
    } 

    if (!obtainedQuestion) {
        const error = new HttpError('Question not found.', 404);
        return next(error);
    }

    try {
        await Question.findByIdAndRemove(questionId);
    } catch (err) {
        const error = new HttpError('Something went wrong, could not delete the question.', 500);
        return next(error);
    };

    res.status(200).json({message: 'Question deleted successfully.'});
}

const updateQuestion = async(req, res, next) => {
    const {category, type, question, answer, link, user_id} = req.body;
    const questionId = req.params.qid;
    let obtainedQuestion;

    try {
        obtainedQuestion = await Question.findById(questionId);
    }catch (err) {
        const error = new HttpError('Something went wrong, could not update the question.', 500);
        return next(error);
    } 

    if (!obtainedQuestion) {
        const error = new HttpError('Question not found in database.', 404);
        return next(error);
    }

    obtainedQuestion.category = category;
    obtainedQuestion.type = type;
    obtainedQuestion.question = question;
    obtainedQuestion.answer = answer;
    obtainedQuestion.link = link;
    obtainedQuestion.user_id = user_id;
    try {
        await obtainedQuestion.save();
    } catch (err) {
        const error = new HttpError('Something went wrong, could not update the question.', 500);
        return next(error);
    };

    // res.status(200).json({message: 'Question updated successfully.'});
    res.status(201).json(obtainedQuestion);
}

exports.createQuestion = createQuestion;
exports.getQuestionById = getQuestionById;
exports.deleteQuestion = deleteQuestion;
exports.updateQuestion = updateQuestion;
