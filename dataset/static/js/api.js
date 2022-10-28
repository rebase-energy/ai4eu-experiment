


const inputForm = document.getElementById('input_form');
const inputName = document.getElementById('input_name');
const inputAsset = document.getElementById('input_asset');
const btnDownload = document.getElementById('btn_download');
const errorText = document.getElementById('error_text');


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

    const name = inputName.value;
    const asset = inputAsset.value
    console.log("submit");
    const result = await getData(name, asset);
    console.log('result :>> ', result);

    const trainDatasets = makeDatasets(result.data.train);
    const validDatasets = makeDatasets(result.data.valid);


    trainChart.data = {datasets: trainDatasets};
    validChart.data = {datasets: validDatasets};
    trainChart.update();
    validChart.update();
}


const getData = async (name, asset) => {
    try {
        errorText.style.display = 'none';
        btnDownload.style.opacity = 0.5;
        btnDownload.style.pointerEvents = 'none';
        const resp = await fetch(`/dataset?name=${name}&asset=${asset}`)
        return await resp.json();
    }
    catch {
        errorText.style.display = 'inline-block';
    }
    finally {
        btnDownload.style.opacity = 1;
        btnDownload.style.pointerEvents = 'auto';
    }

}