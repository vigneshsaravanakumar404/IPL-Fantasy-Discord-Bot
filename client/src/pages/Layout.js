import { Outlet, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { UserContext } from './../UserContext.js';
import Logo from './../images/Logo.png';
import './../styles/Layout.css';

function Navbar() {
    const { username, setUsername } = useContext(UserContext);
    const navigate = useNavigate();

    if(username != null)
    {
        return(
            <div>
                <p>{ username }</p>
            </div>
        );
    }
    else
    {
        return(
            <div id='layout-navbar'>
                <img id='layout-navbar-logo' src={Logo} alt=''/>
                <p class='layout-navbar-link' onClick={() => {
                    navigate('/');
                }}>Home</p>
                <p class='layout-navbar-link' onClick={() => {
                    navigate('/players');
                }}>Player Rankings</p>
                <button id='layout-logout' onClick={() => {
                    setUsername(null);
                    navigate('login');
                }}>Log Out</button>
            </div>
        );
    }
}

function Footer() {
    return (
        <p id='layout-footer'>Designed and Developed by Tejas Raghuram. Rules by Kaushal Krishnamurthy.</p>
    );
}

function Layout() {
    return(
        <div>
            <Navbar/>
            <div id='layout-buffer'/>
            <Outlet/>
            <Footer/>
        </div>
    );
}

export default Layout;