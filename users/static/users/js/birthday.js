const daySelect = document.getElementById('day');
const monthSelect = document.getElementById('month');
const yearSelect = document.getElementById('year');

for (let i = 1; i <= 31; i++) {
  const option = document.createElement('option');
  option.text = i;
  option.value = i;
  daySelect.add(option);
}

for (let i = 1; i <= 12; i++) {
  const option = document.createElement('option');
  option.text = 'Month ' + i;
  option.value = i;
  monthSelect.add(option);
}

const currentYear = new Date().getFullYear();
for (let i = currentYear; i >= 1960; i--) {
  const option = document.createElement('option');
  option.text = i;
  option.value = i;
  yearSelect.add(option);
}