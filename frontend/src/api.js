// /Users/apichet/quantum_lotto/frontend/src/api.js
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export const fetchPrediction = async () => {
  const res = await axios.get(`${BASE_URL}/predict-lotto`);
  return res.data;
};
