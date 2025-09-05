import React from "react";

function EmailTable({ emails }) {
  return (
    <table border="1" cellPadding="8" style={{ width: "100%", marginTop: "20px" }}>
      <thead>
        <tr>
          <th>Sender</th>
          <th>Subject</th>
          <th>Priority</th>
          <th>Sentiment</th>
          <th>AI Response</th>
        </tr>
      </thead>
      <tbody>
        {emails.map((e, i) => (
          <tr key={i}>
            <td>{e.sender}</td>
            <td>{e.subject}</td>
            <td>{e.priority}</td>
            <td>{e.sentiment}</td>
            <td>
              <textarea
                defaultValue={e.ai_response}
                style={{ width: "300px", height: "100px" }}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default EmailTable;
