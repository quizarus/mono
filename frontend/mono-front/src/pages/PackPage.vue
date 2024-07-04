<template>
  <div>
    <q-expansion-item
      v-for="round in rounds"
      :key="round.name"
      :label="round.name"
      dense
      default-open
    >
      <q-expansion-item
        v-for="theme in round.themes"
        :key="theme.name"
        :label="theme.name"
        icon="mdi-chevron-right"
        dense
        default-open
      >
        <q-table
          :rows="theme.questions"
          :columns="questionColumns"
          row-key="uuid"
          dense
          flat
        >
          <template v-slot:body-cell(answer)="props">
            {{ props.value.answer }}
          </template>
          <template v-slot:body-cell(attachments)="props">
            <template v-if="props.value.attachments && (props.value.attachments.content || props.value.attachments.post_content)">
              <a
                v-if="props.value.attachments.content"
                :href="props.value.attachments.content"
                target="_blank"
              >
                Ссылка
              </a>
              <a
                v-if="props.value.attachments.post_content"
                :href="props.value.attachments.post_content"
                target="_blank"
              >
                Ссылка
              </a>
            </template>
            <template v-else>
              <span>-</span>
            </template>
          </template>
        </q-table>
      </q-expansion-item>
    </q-expansion-item>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rounds: [],
      questionColumns: [
        {
          name: 'text',
          required: true,
          label: 'Вопрос',
          align: 'left',
          field: 'text',
          sortable: true
        },
        {
          name: 'answer',
          required: true,
          label: 'Ответ',
          align: 'left',
          field: 'answer',
          sortable: true
        },
        {
          name: 'attachments',
          required: true,
          label: 'Вложение',
          align: 'left',
          field: 'attachments',
          sortable: true
        }
      ]
    };
  },
  mounted() {
    const url = 'https://api.jsonbin.io/v3/b/64897e9e8e4aa6225eae2784/latest';
    const headers = {
      'X-Master-Key': '$2b$10$tbMk05zyxmDvE5DcGqrrleMCToy2s7NVzmpMhZ8VqWzIHepXp3iXK'
    };

    axios.get(url, { headers })
      .then(response => {
        const jsonData = response.data.record;
        this.rounds = jsonData.rounds;
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });
  }
};
</script>
