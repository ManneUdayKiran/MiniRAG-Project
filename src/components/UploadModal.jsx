import React, { useState } from "react";
import { Modal, Tabs, Upload, Button, Input, Spin, message } from "antd";
import { UploadOutlined, LinkOutlined } from "@ant-design/icons";

const { TabPane } = Tabs;

const UploadModal = ({ visible, onClose, onUpload, onAddUrl, urlLoading }) => {
  const [fileList, setFileList] = useState([]);
  const [url, setUrl] = useState("");

  const handleFileChange = ({ fileList }) => {
    setFileList(fileList);
  };

  const handleUpload = () => {
    if (fileList.length === 0)
      return message.warning("Select file(s) to upload");
    onUpload(fileList);
    setFileList([]);
    onClose();
  };

  const handleAddUrl = () => {
    if (!url) return message.warning("Enter a URL");
    onAddUrl(url);
    setUrl("");
    onClose();
  };

  return (
    <Modal
      open={visible}
      onCancel={onClose}
      footer={null}
      title="Add to Knowledge Base"
      destroyOnClose
    >
      <Tabs defaultActiveKey="file">
        <TabPane
          tab={
            <span>
              <UploadOutlined />
              Upload File
            </span>
          }
          key="file"
        >
          <Upload
            multiple
            beforeUpload={() => false}
            onChange={handleFileChange}
            fileList={fileList}
          >
            <Button icon={<UploadOutlined />}>Select File(s)</Button>
          </Upload>
          <Button
            type="primary"
            style={{ marginTop: 16, width: "100%" }}
            onClick={handleUpload}
          >
            Upload
          </Button>
        </TabPane>
        <TabPane
          tab={
            <span>
              <LinkOutlined />
              Add URL
            </span>
          }
          key="url"
        >
          <Input
            placeholder="Paste a URL (web page, article, etc.)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ marginBottom: 12 }}
            disabled={urlLoading}
          />
          <Button
            type="primary"
            loading={urlLoading}
            style={{ width: "100%" }}
            onClick={handleAddUrl}
          >
            Add URL
          </Button>
        </TabPane>
      </Tabs>
    </Modal>
  );
};

export default UploadModal;
