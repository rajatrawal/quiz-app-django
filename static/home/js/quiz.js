document.querySelector('.background_div').style.height = window.height;
let answerInput = Array.from(document.getElementsByClassName('answerInput'));
let click_uid, uid;
var questionP = $('.questionP');
var createObj = true;

async function loadAttendedQuestionData(uid) {

    await fetch(`/loadAttendedQuestionData/${uid}`).then(
        (response) => {
            return response.json();
        }
    ).then((data) => {
        console.log(data);
        if (data['status'] == 200) {
            console.log(data);
            createObj = false;
            for (i of data['payload']) {
                answer = document.getElementById(i['uid']);
                answer.disabled = true;
                if (i['isCorrect'] == 'True') {
                    answer.parentNode.classList.add('list-group-item-success');
                    answer.parentNode.classList.remove('list-group-item-primary');

                }
                if (i['isSelected'] == 'true') {
                    answer.checked = true;
                    if (i['isCorrect'] == 'False') {
                        answer.parentNode.classList.add('list-group-item-danger');
                        answer.parentNode.classList.remove('list-group-item-primary');
                        questionP.get(0).classList.add('text-danger');
                    }
                    else {
                        questionP.get(0).classList.add('text-success');
                    }
                }
            }
        }
    })
}

loadAttendedQuestionData(questionP.get(0).id);

async function giveCorrectAnswer(array) {
    for (answer of array) {
        answer.disabled = true;
        uid = answer.id;
        let request = await fetch(`/checkAnswer/${uid}/false`).then((response) => {
            return response.json();
        }).then((data) => {
            if (data['is_correct'] === 'true') {
                answer.parentNode.classList.add('list-group-item-success');
            }

        })
    }
}

answerInput.forEach((e, i) => {
    e.addEventListener('click',
        (e) => {
            uid = e.target.id;
            fetch(`/checkAnswer/${uid}/${createObj}`).then((response) => {
                response.json().then((data) => {
                    if (data['status'] == 200) {
                        if (data['is_correct'] == 'true') {
                            e.target.parentNode.classList.add('list-group-item-success');
                            questionP.addClass('text-success');
                            giveAlert('alertDiv', 'success', 'Congo! Write Answer.');
                            document.getElementById('marks').innerHTML = data['marks'];
                        }
                        else {
                            e.target.parentNode.classList.add('list-group-item-danger');
                            questionP.addClass('text-danger');
                            giveAlert('alertDiv', 'danger', 'So Sad ! Wrong Answer.');

                        }
                        answerInput = Array.from(document.getElementsByClassName('answerInput'));
                        giveCorrectAnswer(answerInput);
                        e.target.parentNode.classList.remove('list-group-item-primary');
                    }
                    else {
                        giveAlert('alertDiv', 'danger', "Very Smart! Don't Try To Manipulate");
                    }


                })
            })

        }
    )
})
