function deleteEntry(entryId) {
  fetch("/delete-entry", {
    method: "POST",
    body: JSON.stringify({ entryId: entryId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
