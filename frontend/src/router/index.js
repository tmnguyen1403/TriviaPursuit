import { Routes, Route} from 'react-router-dom';

import Question from '../pages/Question';
import QuestionCreate from '../pages/QuestionCreate';
import QuestionEdit from '../pages/QuestionEdit';

const MyRouter = () => {

    return (
        <Routes>
            <Route path="/" element={<Question />} />
            <Route path="/questions/create" element={<QuestionCreate />} />
            <Route path="/questions/:id/edit" element={<QuestionEdit />} />
        </Routes>
    )
}

export default MyRouter;