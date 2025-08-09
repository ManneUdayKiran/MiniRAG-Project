import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Layout,
  Button,
  Input,
  Typography,
  Divider,
  message,
  Spin,
} from "antd";
import { PlusOutlined } from "@ant-design/icons";
import UploadModal from "./components/UploadModal";
import "./App.css";

const { Header, Content, Footer } = Layout;
const { Title, Paragraph } = Typography;

function App() {
  const [fileList, setFileList] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [trackedFiles, setTrackedFiles] = useState([]);
  const [trackedUrls, setTrackedUrls] = useState([]);
  const [refreshKb, setRefreshKb] = useState(0);
  // Fetch tracked files and URLs
  useEffect(() => {
    const fetchKb = async () => {
      const filesRes = await axios.get("http://127.0.0.1:8000/list_files");
      setTrackedFiles(filesRes.data.files || []);
      const urlsRes = await axios.get("http://127.0.0.1:8000/list_urls");
      setTrackedUrls(urlsRes.data.urls || []);
    };
    fetchKb();
  }, [refreshKb]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [urlLoading, setUrlLoading] = useState(false);

  // Modal-based upload/URL add handlers
  const handleModalUpload = async (modalFileList) => {
    // Only upload when user selects files (not on every change)
    if (!modalFileList || modalFileList.length === 0) return;
    const formData = new FormData();
    modalFileList.forEach((f) => {
      if (f.originFileObj) formData.append("files", f.originFileObj);
    });
    try {
      await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      message.success("Files uploaded and processed!");
      setRefreshKb((r) => r + 1);
    } catch (err) {
      message.error("Upload failed.");
    }
  };

  const handleModalAddUrl = async (url) => {
    if (!url) return;
    setUrlLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/add_url", { url });
      if (res.data.status === "success") {
        message.success(`URL content added! Chunks: ${res.data.chunks_added}`);
      } else {
        message.error(
          "Failed to add URL: " + (res.data.error || "Unknown error")
        );
      }
    } catch (err) {
      message.error("Failed to add URL.");
    } finally {
      setUrlLoading(false);
      setRefreshKb((r) => r + 1);
    }
  };

  // Remove old upload handler (now handled in modal)

  const handleAsk = async () => {
    if (!question) return;
    setAnswer("");
    setContext("");
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("question", question);
      const res = await axios.post("http://127.0.0.1:8000/ask", formData);
      setAnswer(res.data.answer);
      setContext(res.data.context);
    } catch (err) {
      setAnswer("Error getting answer from backend.");
      setContext("");
    } finally {
      setLoading(false);
    }
  };

  // Delete file from backend and refresh
  const handleDeleteFile = async (filename) => {
    await axios.delete("http://127.0.0.1:8000/delete_file", {
      params: { filename },
    });
    setRefreshKb((r) => r + 1);
  };

  // Delete URL from backend and refresh
  const handleDeleteUrl = async (url) => {
    await axios.delete("http://127.0.0.1:8000/delete_url", { data: { url } });
    setRefreshKb((r) => r + 1);
  };

  return (
    <Layout style={{ margin: "0px", minHeight: "99vh" }}>
      <Header className="sticky-header">Mini RAG App</Header>
      <Content className="rag-content">
        <div className="rag-container">
          {/* Hero Section */}
          <div className="hero-section">
            <Title level={2} style={{ textAlign: "center", marginBottom: 8 }}>
              A Mini RAG Project
            </Title>
            <Paragraph
              style={{ textAlign: "center", color: "#555", marginBottom: 24 }}
            >
              Retrieval-Augmented Generation: Ask questions strictly from your
              uploaded files or web URLs. <br />
              <span style={{ color: "#1677ff" }}>
                PDF, DOCX, OCR, and web content supported.
              </span>
            </Paragraph>
            <div
              style={{
                display: "flex",
                gap: 8,
                justifyContent: "center",
                marginBottom: 16,
                flexWrap: "wrap",
              }}
            >
              <Input.Search
                placeholder="Type your question..."
                enterButton="Ask"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onSearch={handleAsk}
                style={{ maxWidth: 400, minWidth: 200 }}
              />
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setModalOpen(true)}
                style={{ minWidth: 120 }}
              >
                Add File / URL
              </Button>
            </div>
          </div>
          <Divider />
          {/* Knowledge Base Section */}
          <Title level={5}>Knowledge Base Files</Title>
          <ul>
            {trackedFiles.map((fname) => (
              <li key={fname} style={{ marginBottom: 4 }}>
                {fname}{" "}
                <Button
                  size="small"
                  danger
                  onClick={() => handleDeleteFile(fname)}
                >
                  Delete
                </Button>
              </li>
            ))}
            {trackedFiles.length === 0 && (
              <li style={{ color: "#888" }}>No files uploaded.</li>
            )}
          </ul>
          <Title level={5}>Knowledge Base URLs</Title>
          <ul>
            {trackedUrls.map((u) => (
              <li key={u} style={{ marginBottom: 4 }}>
                <a href={u} target="_blank" rel="noopener noreferrer">
                  {u}
                </a>{" "}
                <Button size="small" danger onClick={() => handleDeleteUrl(u)}>
                  Delete
                </Button>
              </li>
            ))}
            {trackedUrls.length === 0 && (
              <li style={{ color: "#888" }}>No URLs added.</li>
            )}
          </ul>
          <Divider />
          {/* Answer Section */}
          <Title level={5}>Answer</Title>
          <Spin spinning={loading} tip="Loading answer...">
            <Paragraph>{answer}</Paragraph>
            {/* <Title level={5}>Retrieved Context</Title> */}
            {/* <Paragraph type="secondary">{context}</Paragraph> */}
          </Spin>
        </div>
        {/* Upload/URL Modal */}
        <UploadModal
          visible={modalOpen}
          onClose={() => setModalOpen(false)}
          onUpload={handleModalUpload}
          onAddUrl={handleModalAddUrl}
          urlLoading={urlLoading}
        />
      </Content>
      <Footer style={{ textAlign: "center" }}>Mini RAG Project ©2025</Footer>
    </Layout>
  );
}

export default App;
