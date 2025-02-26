<script setup>
import { useRoute, useRouter } from 'vue-router';
import { ref, onMounted, watchEffect } from 'vue';

const route = useRoute();
const router = useRouter();
const token = ref('');
const statusMessage = ref('');

watchEffect(() => {
  token.value = route.params.token || '';
});

onMounted(async () => {
  if (!token.value) {
    statusMessage.value = 'Invalid token';
    return;
  }

  try {
    const response = await fetch(`http://localhost:8080/centers/verify/${token.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    console.log(data);

    if (data.centerId) {
      localStorage.setItem('centerId', data.centerId);
      statusMessage.value = data.message || 'Verification successful';
      
      // Redirect to /centers/dashboard after successful verification
      setTimeout(() => {
        router.push('/centers/dashboard');
      }, 1000); // Delay for better UX
    } else {
      statusMessage.value = 'Verification failed';
    }
  } catch (error) {
    console.error(error);
    statusMessage.value = 'Verification failed';
  }
});
</script>
