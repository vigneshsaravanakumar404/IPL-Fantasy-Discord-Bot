import { useParams } from 'react-router-dom';
import './../styles/User.css';

function User() {
    let params = useParams();

    return(
        <div>
            <p>This is the user page for {params.user} in {params.league}.</p>
        </div>
    );
}

export default User;