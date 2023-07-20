const mongoose = require('mongoose');
const { validationResult } = require('express-validator');

const Question = require('../models/question');
const User = require('../models/user');
const HttpError = require('../models/http-error');

const createQuestion = async(req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(
        new HttpError('Invalid inputs passed, please check your data.', 422)
      );
    }

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

    let user;
    try {
      user = await User.findById(user_id);
    } catch (err) {
      const error = new HttpError(
        'Creating question failed, please try again.',
        500
      );
      return next(error);
    }

    if (!user) {
        const error = new HttpError('Could not find user for provided id.', 404);
        return next(error);
    }

    try {
        const sess = await mongoose.startSession();
        sess.startTransaction();
        await createdQuestion.save({ session: sess }); 
        user.questions.push(createdQuestion); 
        await user.save({ session: sess }); 
        await sess.commitTransaction();

    } catch (err) {
        const error = new HttpError(
            'Creating question failed, please try again.',
            500
        );
        return next(error);
    }

    res.status(201).json({question: createdQuestion});
}

const getQuestionById = async(req, res, next) => {
    const questionId = req.params.qid;
    let obtainedQuestion;
    try {
        obtainedQuestion = await Question.findById(questionId);
    }catch (err) {
        const error = new HttpError(
            'Something went wrong, could not find the question Id.', 
            500
        );
        return next(error);
    } 

    if (!obtainedQuestion) {
        const error = new HttpError(
            'Could not find a question for the provided Id', 
            404
        );
        return next(error);
    }

    res.status(200).json({obtainedQuestion: obtainedQuestion.toObject({ getters: true })});
}

const getQuestionByUserId = async (req, res, next) => {
    const creatorId = req.params.uid;
    let userWithQuestions;
    try {
        userWithQuestions = await Question.find({user_id: creatorId});
    } catch (err) {
        const error = new HttpError(
            'Fetching questions failed, please try again later.', 
            500
        );
        return next(error);
    }
    if (!userWithQuestions || userWithQuestions.length === 0) {
        return next (new HttpError(
            'Could not find the questions for the provided user id.', 
            404)
        );
    }

    res.status(200).json({questionsByUserId: userWithQuestions.map(question => question.toObject({getters: true}))});
}

const getQuestionByCategory = async (req, res, next) => {
    const questionCategory = req.params.cid;
    let categoryWithQuestions;
    try {
        categoryWithQuestions = await Question.find({category: questionCategory});
        console.log("Getting question for ", questionCategory);
    } catch (err) {
        const error = new HttpError(
            'Fetching questions failed, please try again later.', 
            500
        );
        return next(error);
    }
    if (!categoryWithQuestions || categoryWithQuestions.length === 0) {
        return next (new HttpError(
            'Could not find the questions for the provided user category.', 
            404)
        );
    }

    res.status(200).json({questionsByCategory: categoryWithQuestions.map(question => question.toObject({getters: true}))});
}

const deleteQuestion = async(req, res, next) => {

    const questionId = req.params.qid;
    let obtainedQuestion;

    try {
        obtainedQuestion = await Question.findById(questionId).populate('user_id');
    }catch (err) {
        const error = new HttpError(
            'Something went wrong, could not delete the question.', 
            500
        );
        return next(error);
    } 

    if (!obtainedQuestion) {
        const error = new HttpError('Question not found.', 404);
        return next(error);
    }

    try {
        const sess = await mongoose.startSession();
        sess.startTransaction();
        await obtainedQuestion.deleteOne({session: sess});
        obtainedQuestion.user_id.questions.pull(obtainedQuestion);
        await obtainedQuestion.user_id.save({session: sess});
        await sess.commitTransaction();
    } catch (err) {
        const error = new HttpError(
            'Something went wrong, could not delete the question.', 
            500
        );
        return next(error);
    };

    res.status(200).json({message: 'Question deleted successfully.'});
}

const updateQuestion = async(req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(
        new HttpError('Invalid inputs passed, please check your data.', 422)
      );
    }    

    const {category, type, question, answer, link, user_id} = req.body;
    const questionId = req.params.qid;
    let obtainedQuestion;

    try {
        obtainedQuestion = await Question.findById(questionId);
    }catch (err) {
        const error = new HttpError(
            'Something went wrong, could not update the question.', 
            500
        );
        return next(error);
    } 

    if (!obtainedQuestion) {
        const error = new HttpError(
            'Question not found in database.', 
            404
        );
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
        const error = new HttpError(
            'Something went wrong, could not update the question.', 
            500
        );
        return next(error);
    };

    res.status(200).json({updatedQuestion: obtainedQuestion.toObject({getters: true})});
}

exports.createQuestion = createQuestion;
exports.getQuestionById = getQuestionById;
exports.getQuestionByUserId = getQuestionByUserId;
exports.getQuestionByCategory = getQuestionByCategory;
exports.deleteQuestion = deleteQuestion;
exports.updateQuestion = updateQuestion;
