import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import apiList from "../../api.json";

const API_URL = import.meta.env.VITE_API_BASE_URL;

export const loginUser = createAsyncThunk(
  "auth/login",
  async ({ username, password }, { rejectWithValue }) => {
    try {
      // ✅ Build API endpoint dynamically
      const loginEndpoint = `${API_URL}${apiList.auth.login}`;
      

      const { data } = await axios.post(loginEndpoint, {
        username,
        password,
      });

      // ✅ Store tokens & username in localStorage
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      localStorage.setItem("username", username);

      return { username };
    } catch (err) {
      if (err.response && err.response.data.non_field_errors) {
        return rejectWithValue(err.response.data.non_field_errors[0]);
      } else if (err.response && err.response.data.detail) {
        return rejectWithValue(err.response.data.detail);
      } else {
        return rejectWithValue("Something went wrong");
      }
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: localStorage.getItem("username") || null,
    loading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      localStorage.clear();
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload.username;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Invalid credentials";
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
