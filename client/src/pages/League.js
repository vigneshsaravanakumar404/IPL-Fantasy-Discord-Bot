import { useParams } from 'react-router-dom';
import './../styles/League.css';

function League() {
    let params = useParams();

    return(
        <div>
            <p>This is the league page for {params.league}.</p>
        </div>
    );
}

export default League;