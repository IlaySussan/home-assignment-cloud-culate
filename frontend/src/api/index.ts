import axios from 'axios';

const API_URL = import.meta.env.VITE_BACKEND_API_URL as string;

export const fetchItems = async () => {
  try {
    const response = await axios.get(`${API_URL}/architectures`);
    return response.data;
  } catch (error) {
    console.error('Error fetching items:', error);
    throw error;
  }
};

export const scrapeUrl = async (url: string) => {
  try {
    const response = await axios.post(`${API_URL}/scrape`,{url});
    return response.data;
  } catch (error) {
    console.error('Error scraping URL:', error);
    throw error;
  }
}

export const deleteAllScrapedArchitectures = async () => {
  try {
    const response = await axios.delete(`${API_URL}/architectures`);
    return response.data;
  } catch (error) {
    console.error('Error deleting scraped architectures:', error);
    throw error;
  }
}