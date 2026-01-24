import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import toast from "react-hot-toast";

const AppContext = createContext();
export const AppContextProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [loadingUser, setLoadingUser] = useState(true);

  const backendUrl = import.meta.env.VITE_SERVER_URL;
  axios.defaults.baseURL = backendUrl;

  const fetchUser = async () => {
    try {
      const { data } = await axios.get("/protected", {
        headers: { Authorization: token },
      });
      if (data.success) {
        setUser(data.user);
      } else {
        toast.error(data);
      }
    } catch (error) {
      toast.error(error);
    } finally {
      setLoadingUser(false);
    }
  };

  const createNewMessage = async () => {
    try {
      if (!user) {
        return toast("Login to create a new message");
      }
      navigate("/");
      const { data } = await axios.get("/messages", {
        headers: { Authorization: "Bearer " + token },
      });
      console.log("data", data);
      await fetchUserMessages();
    } catch (error) {
      toast.error(error.message);
    }
  };

  const fetchUserMessages = async () => {
    try {
      const { data } = await axios.get(`/messages/${user.id}`, {
        headers: { Authorization: token },
      });
      console.log("data2", data);
      if (data.success) {
        setMessages(data.messages);
      }
    } catch (error) {
      toast.error(`error ${error}`);
    }
  };

  useEffect(() => {
    if (user) {
      fetchUserMessages();
    }
  }, [user]);

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setUser(null);
    }
  }, [token]);

  const value = {
    navigate,
    user,
    fetchUser,
    setUser,
    messages,
    setMessages,
    createNewMessage,
    loadingUser,
    fetchUserMessages,
    token,
    setToken,
    axios,
    setLoadingUser,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useAppContext = () => useContext(AppContext);
