const myData = {
    firstName: 'Kelechi',
    lastName : 'Apugo',
    email :'laviedegeorge1292@gmail.com',
    internId :'HNG-06129',
    scriptingLanguage:'javascript'
}


const showInfo = ({firstName, lastName, email, internId, scriptingLanguage})=>{
    const info = `Hello World, this is ${firstName} ${lastName} with HNGi7 ID ${internId} using ${scriptingLanguage} for stage 2 task and ${email}`;
    return info;
}

console.log(showInfo(myData));