const express = require('express');


const questionsController = require('../controllers/questions-controller');
const router = express.Router();


router.post('/', questionsController.createQuestion);
router.get('/:qid', questionsController.getQuestionById);
router.get('/user/:uid', questionsController.getQuestionByUserId);
// router.get('/category/:cid', questionsController.getQuestionByCategory);
router.get('user/:uid/:cid', questionsController.getQuestionByCategory);
router.delete('/:qid', questionsController.deleteQuestion);
router.patch('/:qid', questionsController.updateQuestion);

module.exports = router;
