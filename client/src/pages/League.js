import { useNavigate, useParams } from 'react-router-dom';
import './../styles/League.css';

function User(props) {
    const navigate = useNavigate();
    const params = useParams();

    return(
        <div class='league-user-body' onClick={() => {
            navigate('/' + params.league + '/' + props.username)
        }}>
            <div class='league-user-rank-body'>
                <p class='league-user-rank'>1</p>
            </div>
            <p class='league-user-name'>{props.username}</p>
            <p class='league-user-points'>{props.points}</p>
        </div>
    );
}

function League() {
    const params = useParams();

    return(
        <div id='league-content'>
            <h1>{params.league}</h1>
            <User username={'TejasRaghuram'} points={20349}/>
            <User username={'IshaanSinha'} points={19872}/>
            <User username={'VigneshSaravanakumar'} points={19428}/>
        </div>
    );
}

export default League;