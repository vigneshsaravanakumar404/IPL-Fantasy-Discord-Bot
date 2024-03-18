import { useState } from "react";
import "./../styles/Admin.css";

function Match(props) {
  return (
    <div class="admin-fixture">
      <h3 class="admin-match">{props.fixture}</h3>
      <p class="admin-match">{props.status}</p>
      <button
        class="admin-add"
        onClick={() => {
          // add match
        }}
      >
        Add Match
      </button>
    </div>
  );
}

function Admin() {
  const [verified, setVerified] = useState(false);

  return (
    <div id="admin-content">
      <h2 id="admin-prompt">Enter Password: </h2>
      <input id="admin-password" type="password" name="password"></input>
      <button
        id="admin-submit"
        onClick={() => {
          if (document.getElementById("admin-password").value === "password") {
            setVerified(true);
          }
        }}
      >
        Submit
      </button>
      {verified && (
        <div id="admin-portal">
          <h1>Welcome, Admin</h1>
          <Match fixture="RCB vs SRH" status="RCB Won" />
          <Match fixture="CSK vs GT" status="CSK Won" />
        </div>
      )}
    </div>
  );
}

export default Admin;
