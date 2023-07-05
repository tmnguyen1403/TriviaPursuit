const express = require('express');

const questionsControllers = require('../controllers/questions-controller');
const router = express.Router();

router.post('/', questionsControllers.createQuestion);
router.get('/:qid', questionsControllers.getQuestionById);
router.delete('/:qid', questionsControllers.deleteQuestion);
router.patch('/:qid', questionsControllers.updateQuestion);

module.exports = router;
