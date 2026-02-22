function DownloadButton({ data }) {
  if (!data) return null;

  const download = () => {
    const blob = new Blob(
      [JSON.stringify(data, null, 2)],
      { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "money_muling_report.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  return <button onClick={download}>Download JSON Report</button>;
}

export default DownloadButton;
