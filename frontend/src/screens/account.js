import React, { useState, useEffect } from "react";
import axios from "axios";

function Test() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://128.199.176.152/address")
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div>
      <h1>Data from API:</h1>
      {data && <div>{data}</div>}
    </div>
  );
}

export default Test;
