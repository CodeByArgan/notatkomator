import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.response.use(
  async (response) => {
    await new Promise((res) => setTimeout(res, 300));
    return response;
  },
  async (error) => {
    await new Promise((res) => setTimeout(res, 300));
    return Promise.reject(error);
  }
);

export const axiosGet = async <T = unknown>({
  url,
}: {
  url: string;
}): Promise<T> => {
  try {
    const response = await api.get<T>(url);
    return response.data;
  } catch (error) {
    console.error(`Error when get'ing ${url} message ${error}`);
    throw error;
  }
};

export const axiosPost = async <T = unknown, U = unknown>({
  url,
  data,
}: {
  url: string;
  data: U;
}): Promise<T> => {
  try {
    const response = await api.post<T>(url, data);
    return response.data;
  } catch (error) {
    console.error(`Error when post'ing ${url} message ${error}`);
    throw error;
  }
};
