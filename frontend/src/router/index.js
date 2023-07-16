import { Routes, Route} from 'react-router-dom';

import Home from '../pages/Home';
import Signup from '../pages/Signup';
import Login from '../pages/Login';
import Question from '../pages/Question';
import QuestionCreate from '../pages/QuestionCreate';
import QuestionEdit from '../pages/QuestionEdit';

const MyRouter = () => {

    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sign-up" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/questions" element={<Question />} />
            <Route path="/questions/create" element={<QuestionCreate />} />
            <Route path="/questions/:id/edit" element={<QuestionEdit />} />
        </Routes>
    )
}

export default MyRouter;