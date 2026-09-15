import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProfile = async () => (await api.get('/profile')).data;
export const updateProfile = async (data) => (await api.put('/profile', data)).data;

export const askChat = async (query) => (await api.post('/chat', { query })).data;

export const checkEligibility = async (company_name = null) => 
  (await api.post('/placement/check-eligibility', { company_name })).data;

export const compareCompanies = async (company_names) => 
  (await api.post('/placement/compare', { company_names })).data;

export const getCompanies = async () => (await api.get('/companies')).data;

export const getCareerRoadmap = async (target_role, current_skill_level = "Beginner", preparation_time = "3 Months") => 
  (await api.post('/career/roadmap', { target_role, current_skill_level, preparation_time })).data;

export const generateInterviewPrep = async (target_role, topic = "All Topics", difficulty = "Intermediate") => 
  (await api.post('/interview/generate', { target_role, topic, difficulty })).data;

export const getResumeGuidance = async (target_role, skills, projects = "") => 
  (await api.post('/resume/guidance', { target_role, skills, projects })).data;

export const getDocuments = async () => (await api.get('/documents')).data;

export const uploadDocument = async (formData) => 
  (await api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })).data;

export const deleteDocument = async (docId) => (await api.delete(`/documents/${docId}`)).data;
export const reprocessDocument = async (docId) => (await api.post(`/documents/${docId}/reprocess`)).data;

export const getKBStatus = async () => (await api.get('/knowledge-base/status')).data;
export const rebuildKBIndex = async () => (await api.post('/knowledge-base/rebuild')).data;

export const testRetrieval = async (query, top_k = 5) => 
  (await api.post('/retrieval/test', { query, top_k })).data;

export default api;
