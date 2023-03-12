const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
  document.documentElement.setAttribute('data-theme', currentTheme);

  if (currentTheme === 'dark') {
    toggleSwitch.checked = true;
  }
}

function switchTheme(e) {
  if (e.target.checked) {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  }
}

toggleSwitch.addEventListener('change', switchTheme, false);

const form = document.getElementById('summarize-form');
const outputDiv = document.getElementById('output-container');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const text = document.getElementById('input-text').value.trim();

  fetch('/', {
    method: 'POST',
    body: JSON.stringify({ text: text }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then((response) => response.json())
  .then((data) => {
    outputDiv.innerHTML = '';

    for (let method in data) {
      const summary = data[method];
      const methodDiv = document.createElement('div');
      methodDiv.classList.add('method');
      methodDiv.innerHTML = `<h3>${method}</h3><textarea>${summary}</textarea>`;
      outputDiv.appendChild(methodDiv);
    }
  })
  .catch((error) => console.error('Error:', error));
});
