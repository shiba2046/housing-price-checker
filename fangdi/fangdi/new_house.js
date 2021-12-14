function doQuery() {

    //写日志

    //addLog("一手房","房源查询");

    $.ajax({

        type: "POST",
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        url: "http://www.fangdi.com.cn/service/freshHouse/getHosueList.action",
        data: param,
        dataType: "json",
        success: function(data) {
            var listdata = data.htmlView;
            console.log(listdata)
        },

        error: function() {}

    });
}

param = {
    districtID: "",
    dicRegionID: "",
    stateID: "",
    houseAreaID: "",
    dicAvgpriceID: "",
    dicPositionID: "",
    houseTypeID: "",
    address: "",
    openingID: "",
    projectName: "",
    currentPage: "1",
};
const data = new TextEncoder().encode(
    JSON.stringify(param)
)

const http = require('http');
const options = {
    hostname: 'www.fangdi.com.cn',
    path: '/service/freshHouse/getHosueList.action',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }

}

let result = ''

const req = http.request(options, res => {
    console.log(`statusCode: $(res.statusCode)`)

    res.on('data', d => {
        //process.stdout.write(eval(d))
        result = d;
    })
})

req.on('error', error => {
    console.error(error)
})

req.write(data)

req.end()