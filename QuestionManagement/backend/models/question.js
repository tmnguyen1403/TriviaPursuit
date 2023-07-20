const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const questionSchema = new Schema ({
    category: { type: String, required: true },
    type: { type: String, required: true },
    question: { type: String, required: true },
    answer: { type: String, required: true },
    link: { type: String, required: false },
    user_id: { type: mongoose.Types.ObjectId, required: true, ref: 'User' },
    createdAt: { type: Date, required: false, default: Date.now }
});

module.exports = mongoose.model('Question', questionSchema);