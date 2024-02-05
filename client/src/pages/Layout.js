import { Outlet } from 'react-router-dom';
import './../styles/Layout.css';

function Layout() {
    return(
        <div>
            <p>This is the header.</p>
            <Outlet/>
            <p>This is the footer.</p>
        </div>
    );
}

export default Layout;