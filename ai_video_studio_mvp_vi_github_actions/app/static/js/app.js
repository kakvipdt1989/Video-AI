setTimeout(() => {
  document.querySelectorAll('.alert-dismissible').forEach((el) => {
    const alert = bootstrap.Alert.getOrCreateInstance(el);
    alert.close();
  });
}, 5000);
