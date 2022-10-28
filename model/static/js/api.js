
let predTimestamp = null;


const inputForm = document.getElementById('input_form');
const trainInput = document.getElementById('train_file');
const predInput = document.getElementById('pred_file');
const btnPredict = document.getElementById('btn_predict');
const lastRunSpan = document.getElementById('last_run_span');

const colors = [
    '#003f5c',
    '#7a5195',
    '#ef5675',
    '#ffa600',
]

const makeDatasets = (data) => {
    const datasets = []
    let index = 0;
    for (key in data){
        if (key !== 'ref_datetime' && key !== 'valid_datetime'){
            const temp = data[key].map((v, i) => ({
                x: data.valid_datetime[i], //Date.parse(result.data.valid_datetime[i]),
                y: v
            }))
            datasets.push({
                label: key,
                pointRadius: 0,
                data: temp,
                borderColor: colors[index]
            });
            index++;
        }
    }
    return datasets;
}

inputForm.onsubmit = async (e) => {
    e.preventDefault();

    await runPredict();


}

const pollResults = async () => {
    const resp = await fetch('/result');
    if (resp.status === 200){
        const data = await resp.json();
        if (data.timestamp !== predTimestamp){
            const result = data['prediction'];
            const datasets = makeDatasets(result);
            myChart.data = {datasets: datasets};
            myChart.update();
            predTimestamp = data.timestamp;
            lastRunSpan.textContent = `${predTimestamp}`;
        }

    };
    setTimeout(pollResults, 5000);
}

pollResults();


const runPredict = async () => {
    try {
        btnPredict.style.opacity = 0.5;
        btnPredict.style.pointerEvents = 'none';
        const data = new FormData()

        data.append('train_file', trainInput.files[0], trainInput.files[0].name)
        data.append('pred_file', predInput.files[0], predInput.files[0].name)

        const options = {
            method: 'POST',
            body: data
        }
        const resp = await fetch(`/predict`, options);
        return await resp.json();
    }
    catch (e) {
        console.log(e);
    }
    finally {
        btnPredict.style.opacity = 1;
        btnPredict.style.pointerEvents = 'auto';
    }

}