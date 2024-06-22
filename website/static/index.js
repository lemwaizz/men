function deleteCollection(collectionId) {
  fetch("/delete-collection", {
    method: "POST",
    body: JSON.stringify({ collectionId: collectionId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}