import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AddressComponent = () => {
  const [addressData, setAddressData] = useState(null);

  const API_URL = 'https://cors-anywhere.herokuapp.com/http://128.199.176.152/';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(API_URL);
        setAddressData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [API_URL]); // Make sure to include API_URL in the dependency array

  return (
    <div>
      <h1>Address Data</h1>
      {addressData ? (
        <ul>
          {Object.entries(addressData).map(([key, value]) => (
            <li key={key}>
              <strong>{key}:</strong> {value}
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default AddressComponent;
