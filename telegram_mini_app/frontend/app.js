let tg = window.Telegram.WebApp;
let user = tg.initDataUnsafe.user;
let backendUrl = "https://your-render-app.onrender.com"; // Render এ ডেপ্লোয় করার পর এড্রেস দিবেন

// অ্যাপ ইনিশিয়ালাইজ
tg.expand();
tg.enableClosingConfirmation();

// ইউজার ইনফো শো
if (user) {
    document.getElementById('user-info').innerHTML = `
        Welcome, ${user.first_name} ${user.last_name || ''} (@${user.username || 'no_username'})
    `;
    
    // ইউজার ডাটা লোড
    loginUser();
    loadBalance();
    loadTransactions();
} else {
    document.getElementById('user-info').innerHTML = "User data not available";
}

// ইউজার লগইন/রেজিস্টার
function loginUser() {
    fetch(`${backendUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            telegram_id: user.id.toString(),
            username: user.username,
            first_name: user.first_name,
            last_name: user.last_name || ''
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("User logged in:", data.user);
            // রেফারেল লিঙ্ক সেট করুন
            document.getElementById('referral-link').value = 
                `https://t.me/your_bot_username?start=${user.id}`;
        }
    })
    .catch(error => {
        console.error('Login error:', error);
    });
}

// ব্যালেন্স লোড
function loadBalance() {
    fetch(`${backendUrl}/api/wallet/balance/${user.id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('balance').textContent = data.balance.toFixed(2);
        })
        .catch(error => {
            console.error('Balance loading error:', error);
        });
}

// ডিপোজিট ফাংশন
function deposit() {
    const amount = parseFloat(prompt("Enter deposit amount:"));
    if (isNaN(amount) || amount <= 0) {
        alert("Please enter a valid amount");
        return;
    }
    
    fetch(`${backendUrl}/api/wallet/deposit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            telegram_id: user.id.toString(),
            amount: amount
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Deposit successful! New balance: ${data.new_balance}`);
            loadBalance();
            loadTransactions();
        } else {
            alert("Deposit failed");
        }
    })
    .catch(error => {
        console.error('Deposit error:', error);
        alert("Deposit error occurred");
    });
}

// অন্যান্য ফাংশনগুলো একইভাবে ইম্প্লিমেন্ট করুন
function withdraw() {
    // উইথড্র ফাংশন ইম্প্লিমেন্ট করুন
}

function copyReferralLink() {
    // রেফারেল লিঙ্ক কপি করার ফাংশন
}

function claimDailyBonus() {
    // ডেইলি বোনাস ক্লেইম করার ফাংশন
}

function loadTransactions() {
    // ট্রানজ্যাকশন হিস্টরি লোড করার ফাংশন
}